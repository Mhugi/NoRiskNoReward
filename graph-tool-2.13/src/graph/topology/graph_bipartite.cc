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
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#include "graph_filtering.hh"
#include "graph.hh"
#include "graph_properties.hh"

#include <boost/graph/bipartite.hpp>

using namespace std;
using namespace boost;
using namespace graph_tool;

struct get_bipartite
{
    template <class Graph, class VertexIndex, class PartMap>
    void operator()(Graph& g, VertexIndex vertex_index, PartMap part_map,
                    bool& is_bip) const
    {
        unchecked_vector_property_map<default_color_type, VertexIndex>
            part(vertex_index, num_vertices(g));

        is_bip = is_bipartite(g, vertex_index, part);

        int i, N = num_vertices(g);
        #pragma omp parallel for default(shared) private(i) schedule(runtime) if (N > 100)
        for (i = 0; i < N; ++i)
        {
            auto v = vertex(i, g);
            if (!is_valid_vertex(v, g))
                continue;
            part_map[v] = (part[v] == color_traits<default_color_type>::white());
        }
    }

    template <class Graph, class VertexIndex>
    void operator()(Graph& g, VertexIndex vertex_index,
                    dummy_property_map, bool& is_bip) const
    {
        is_bip = is_bipartite(g, vertex_index);
    }
};

bool is_bipartite(GraphInterface& gi, boost::any part_map)
{
    bool is_bip;

    if (part_map.empty())
        part_map = dummy_property_map();

    typedef mpl::push_back<writable_vertex_scalar_properties,
                           dummy_property_map>::type vertex_map_types;

    run_action<graph_tool::detail::never_directed>()
        (gi, std::bind(get_bipartite(), std::placeholders::_1, gi.get_vertex_index(),
                       std::placeholders::_2, std::ref(is_bip)),
         vertex_map_types())(part_map);
    return is_bip;
}
