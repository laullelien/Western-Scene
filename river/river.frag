#version 330 core

in vec3 w_position, w_normal;

uniform vec3 light_dir;

uniform vec3 k_a, k_d, k_s;
uniform float s;

uniform vec3 w_camera_position;

out vec4 out_color;

void main() {
    // Compute all vectors, oriented outwards from the fragment
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, w_normal);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = k_d * max(dot(w_normal, l), .0);
    vec3 specular_color = k_s * pow(max(dot(r, v), .0), s);

    out_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
}