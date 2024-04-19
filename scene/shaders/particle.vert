#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 center;
uniform vec2 size;
uniform float alpha;

in vec3 position;
in vec2 tex_coord;

out vec2 frag_tex_coords;

void main() {
    vec3 camera_right = vec3(view[0][0], view[1][0], view[2][0]);
    vec3 camera_up = vec3(view[0][1], view[1][1], view[2][1]);

    vec3 vertexPosition = center + camera_right * position.x * size.x
    + camera_up * position.y * size.y;

    gl_Position = projection * view * vec4(vertexPosition, 1);

    frag_tex_coords = tex_coord;
}
