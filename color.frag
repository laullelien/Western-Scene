#version 330 core

in vec4 color;
out vec4 out_color;

void main() {
    out_color = color / 2 + vec4(.5, .5, .5, 0);
}
