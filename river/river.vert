#version 330 core

in vec2 position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float time;

out vec3 w_normal;
out vec3 w_position;

void main() {
    vec4 a = vec4(1., .5, .25, .125);
    vec4 deph = vec4(.0, 1.5, 3.1, 4.6);
    vec4 w = vec4(-.125, .25, .5, 1.);
    vec4 kx = vec4(.25, -.5, 1., -2.);
    vec4 ky = vec4(-.30, .55, -1.1, 2.2);
    float height = .0;
    float dx = .0;
    float dy = .0;

    for(int i = 0; i < 4; ++i) {
        height += a[i] * sin(kx[i] * position.x + ky[i] * position.y + w[i] * time + deph[i]);
        dx += a[i] * kx[i] * cos(kx[i] * position.x + ky[i] * position.y + w[i] * time + deph[i]);
        dx += a[i] * ky[i] * cos(kx[i] * position.x + ky[i] * position.y + w[i] * time + deph[i]);
    }

    gl_Position = projection * view * model * vec4(position, height - 2, 1);

    w_normal = cross(vec3(1, 0, dx), vec3(0, 1, dy));
    w_normal = normalize(w_normal);

    w_position = vec3(position, height - 2);
}