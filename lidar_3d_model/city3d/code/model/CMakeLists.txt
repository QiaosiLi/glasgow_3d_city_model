cmake_minimum_required(VERSION 3.1)

get_filename_component(PROJECT_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
project(${PROJECT_NAME})


set(model_HEADERS
        iterators.h
        kdtree_search.h
        map_attributes.h
        map_builder.h
        map_cells.h
        map_circulators.h
        map_copier.h
        map_editor.h
        map_enumerator.h
        map_geometry.h
        map_io.h
        map_serializer_obj.h
        map_serializer_json.h
        map_serializer.h
        map.h
        point_set_io.h
        point_set_serializer_vg.h
        point_set_serializer_ply.h
        point_set_serializer_las.h
        point_set.h
        vertex_group.h
        kdtree/kdTree.h
        kdtree/PriorityQueue.h
        kdtree/QueryGrid.h
        kdtree/vector2D.h
        kdtree/vector3D.h
        )

set(model_SOURCES
        kdtree_search.cpp
        map_builder.cpp
        map_cells.cpp
        map_copier.cpp
        map_editor.cpp
        map_enumerator.cpp
        map_geometry.cpp
        map_io.cpp
        map_serializer_obj.cpp
        map_serializer_json.cpp
        map_serializer.cpp
        map.cpp
        point_set_io.cpp
        point_set_serializer_vg.cpp
        point_set_serializer_ply.cpp
        point_set_serializer_las.cpp
        point_set.cpp
        point_set_geometry.cpp
        kdtree/kdTree.cpp
        )

add_library(${PROJECT_NAME} STATIC ${model_SOURCES} ${model_HEADERS})
set_target_properties(${PROJECT_NAME} PROPERTIES FOLDER "City3D")

set(LASTOOLS_INCLUDE_DIR ${3RD_PARTY_DIR}/3rd_LAStools/LASzip/src ${3RD_PARTY_DIR}/3rd_LAStools/LASlib/inc)
target_include_directories(${PROJECT_NAME} PRIVATE ${LASTOOLS_INCLUDE_DIR})

if (MSVC)
    target_compile_definitions(${PROJECT_NAME} PRIVATE
            _CRT_SECURE_NO_WARNINGS
            _CRT_SECURE_NO_DEPRECATE
            )
endif ()

target_link_libraries(${PROJECT_NAME} basic math 3rd_LAStools 3rd_rply)
