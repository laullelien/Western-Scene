#version 330 core

in vec3 w_position, w_normal;

uniform vec3 light_dir;

uniform vec3 k_a, k_d, k_s;
uniform float s;

out vec4 out_color;

void main() {
    // Compute all vectors, oriented outwards from the fragment
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, w_normal);

    vec3 tex_color = vec3(0.4);
    vec3 diffuse_color = tex_color * max(dot(w_normal, l), .0);

    out_color = vec4(.7 * tex_color, 1) + vec4(diffuse_color, 1);
}