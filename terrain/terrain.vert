#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;
//in vec3 color;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 w_normal;
out vec3 w_position;

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    w_position = position;
    w_normal = normal;
}