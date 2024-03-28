#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;
//in vec3 color;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 color;

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    color = vec4(normal, 0);
}