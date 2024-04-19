#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D normal_map;
uniform vec3 light_dir;
uniform vec3 k_a, k_d, k_s;
uniform vec3 w_camera_position;
uniform float s;

in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

vec4 fog_calc(vec4 shadedColor) {
    // Fog parameters
    float fog_maxdist = 500.0;
    float fog_mindist = 50;
    vec4 fog_colour = vec4(0.6, 0.6, 0.6, 1.0);
    
    // Calculate fog
    float dist = length(w_position - w_camera_position); // This is not it
    float fog_factor = (fog_maxdist - dist) / (fog_maxdist - fog_mindist);
    fog_factor = clamp(fog_factor, 0.0, 1.0);

    return mix(fog_colour, shadedColor, fog_factor);
}

void main() {
    vec3 normal = texture(normal_map, frag_tex_coords).rgb;
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, normal);
    
    vec3 tex_color = texture(diffuse_map, frag_tex_coords).rgb;
    vec3 diffuse_color = tex_color * max(dot(normal, l), .0);

    vec4 shadedColor = vec4(.7 * tex_color, 1) + vec4(diffuse_color, 1);

    out_color = fog_calc(shadedColor); 
}
