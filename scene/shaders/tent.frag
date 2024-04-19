#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D normal_map;
uniform vec3 light_dir;
uniform vec3 k_a, k_d, k_s;
uniform float s;

in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    //out_color = vec4(frag_tex_coords.x, frag_tex_coords.y, 0, 1);
    vec3 normal = texture(normal_map, frag_tex_coords).rgb;
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, normal);
    
    vec3 tex_color = texture(diffuse_map, frag_tex_coords).rgb;
    vec3 diffuse_color = tex_color * max(dot(normal, l), .0);

    out_color = vec4(.7 * tex_color, 1) + vec4(diffuse_color, 1);
}
