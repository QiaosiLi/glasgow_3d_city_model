cmake_minimum_required(VERSION 3.1)

get_filename_component(PROJECT_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
project(${PROJECT_NAME})


set(method_HEADERS
        alpha_shape_CGAL5_4.h
        alpha_shape_mesh.h
        alpha_shape.h
        cgal_types.h
        face_selection.h
        hypothesis_generator.h
        method_global.h
        point_set_region_growing.h
        Modified_Otr2.h
        dbscan.h
        otr2_edge_simplify.h
        regularize_polygon.h
        )

set(method_SOURCES
        alpha_shape_mesh.cpp
        alpha_shape_boundary.cpp
        face_selection.cpp
        face_selection_optimization.cpp
        point_set_normals.cpp
        hypothesis_generator.cpp
        polyfit_info.cpp
        reconstruction.cpp
        method_global.cpp
        point_set_region_growing.cpp
        regularize_polygon.cpp
        otr2_edge_simplify.cpp)


add_library(${PROJECT_NAME} STATIC ${method_SOURCES} ${method_HEADERS})
set_target_properties(${PROJECT_NAME} PROPERTIES FOLDER "City3D")

find_package(CGAL REQUIRED COMPONENTS Core)
if (CGAL_FOUND)
    message(STATUS "Found CGAL: ${CGAL_VERSION}")
    if (CGAL_VERSION VERSION_GREATER_EQUAL "5.4")
        include(${CGAL_USE_FILE})
        message("CGAL_CXX_FLAGS_INIT: ${CGAL_CXX_FLAGS_INIT}")
        add_definitions(${CGAL_CXX_GLAFS_INIT})
        message("CGAL_LIBRARIES: ${CGAL_LIBRARIES}")
        message("CGAL_3RD_PARTY_LIBRARIES: ${CGAL_3RD_PARTY_LIBRARIES}")
        target_link_libraries(${PROJECT_NAME} ${CGAL_LIBRARIES} ${CGAL_3RD_PARTY_LIBRARIES})
    else ()
        message(FATAL_ERROR "CGAL ${CGAL_VERSION} found, but v5.4 or above is required. Please install CGAL v5.4 or above")
    endif ()
else ()
    message(FATAL_ERROR "CGAL is required.")
endif ()

find_package(GMP REQUIRED)
if (GMP_FOUND)
    message("GMP_INCLUDE_DIR: ${GMP_INCLUDE_DIR}")
    message("GMP_LIBRARIES: ${GMP_LIBRARIES}")
    target_link_libraries(${PROJECT_NAME} ${GMP_LIBRARIES})
endif ()

target_include_directories(${PROJECT_NAME} PRIVATE ${POLYFIT_eigen_DIR})

find_package(OpenCV REQUIRED COMPONENTS core imgproc)
target_link_libraries(${PROJECT_NAME} basic math model renderer ${OpenCV_LIBS})