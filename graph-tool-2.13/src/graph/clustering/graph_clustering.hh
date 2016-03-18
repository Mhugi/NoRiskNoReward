// graph-tool -- a general graph modification and manipulation thingy
//
// Copyright (C) 2006-2016 Tiago de Paula Peixoto <tiago@skewed.de>
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// you should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#ifndef GRAPH_CLUSTERING_HH
#define GRAPH_CLUSTERING_HH

#include "config.h"

#include "hash_map_wrap.hh"
#include <boost/mpl/if.hpp>

#ifdef USING_OPENMP
#include "omp.h"
#endif

#ifndef __clang__
#include <ext/numeric>
using __gnu_cxx::power;
#else
template <class Value>
Value power(Value value, int n)
{
    return pow(value, n);
}
#endif

namespace graph_tool
{
using namespace boost;

// calculates the number of triangles to which v belongs
template <class Graph, class VProp>
pair<int,int>
get_triangles(typename graph_traits<Graph>::vertex_descriptor v, VProp& mark,
              const Graph &g)
{
    size_t triangles = 0;

    for (auto n : adjacent_vertices_range(v, g))
    {
        if (n == v)
            continue;
        mark[n] = true;
    }

    for (auto n : adjacent_vertices_range(v, g))
    {
        if (n == v)
            continue;
        for (auto n2 : adjacent_vertices_range(n, g))
        {
            if (n2 == n)
                continue;
            if (mark[n2])
                ++triangles;
        }
    }

    for (auto n : adjacent_vertices_range(v, g))
        mark[n] = false;

    size_t k = out_degree(v, g);
    return make_pair(triangles / 2, (k * (k - 1)) / 2);
}


// retrieves the global clustering coefficient
struct get_global_clustering
{
    template <class Graph>
    void operator()(const Graph& g, double& c, double& c_err) const
    {
        size_t triangles = 0, n = 0;
        pair<size_t, size_t> temp;

#ifdef USING_OPENMP
        size_t n_threads = omp_get_max_threads();
#else
        size_t n_threads = 1;
#endif

        vector<vector<bool>> mask(n_threads);
        for (auto& m : mask)
            m.resize(num_vertices(g), false);

        int i, N = num_vertices(g);
        #pragma omp parallel for default(shared) private(i,temp) \
            schedule(runtime) if (N > 100) reduction(+:triangles, n)
        for (i = 0; i < N; ++i)
        {
            auto v = vertex(i, g);
            if (!is_valid_vertex(v, g))
                continue;

#ifdef USING_OPENMP
            size_t tid = omp_get_thread_num();
#else
            size_t tid = 0;
#endif
            temp = get_triangles(v, mask[tid], g);
            triangles += temp.first;
            n += temp.second;
        }
        c = double(triangles) / n;

        // "jackknife" variance
        c_err = 0.0;
        double cerr = 0.0;

        #pragma omp parallel for default(shared) private(i,temp) \
            schedule(runtime) if (N > 100) reduction(+:cerr)
        for (i = 0; i < N; ++i)
        {
            auto v = vertex(i, g);
            if (!is_valid_vertex(v, g))
                continue;

#ifdef USING_OPENMP
            size_t tid = omp_get_thread_num();
#else
            size_t tid = 0;
#endif
            temp = get_triangles(v, mask[tid], g);
            double cl = double(triangles - temp.first) / (n - temp.second);

            cerr += power(c - cl, 2);
        }
        c_err = sqrt(cerr);
    }
};

// sets the local clustering coefficient to a property
struct set_clustering_to_property
{
    template <class Graph, class ClustMap>
    void operator()(const Graph& g, ClustMap clust_map) const
    {
        typedef typename property_traits<ClustMap>::value_type c_type;
        typename get_undirected_graph<Graph>::type ug(g);
        int i, N = num_vertices(g);

#ifdef USING_OPENMP
        size_t n_threads = omp_get_max_threads();
#else
        size_t n_threads = 1;
#endif

        vector<vector<bool>> mask(n_threads);
        for (auto& m : mask)
            m.resize(num_vertices(g), false);

        #pragma omp parallel for default(shared) private(i) \
            schedule(runtime) if (N > 100)
        for (i = 0; i < N; ++i)
        {
            auto v = vertex(i, g);
            if (!is_valid_vertex(v, g))
                continue;

#ifdef USING_OPENMP
            size_t tid = omp_get_thread_num();
#else
            size_t tid = 0;
#endif
            auto triangles = get_triangles(v, mask[tid], ug); // get from ug
            double clustering = (triangles.second > 0) ?
                double(triangles.first)/triangles.second :
                0.0;

            clust_map[v] = c_type(clustering);
        }
    }

    template <class Graph>
    struct get_undirected_graph
    {
        typedef typename mpl::if_
           <std::is_convertible<typename graph_traits<Graph>::directed_category,
                                directed_tag>,
            const UndirectedAdaptor<Graph>,
            const Graph& >::type type;
    };
};

} //graph-tool namespace

#endif // GRAPH_CLUSTERING_HH
