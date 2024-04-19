#version 330 core

uniform sampler2D diffuse_map;
uniform mat4 model;
uniform vec3 light_dir;
uniform vec3 k_a, k_d, k_s;
uniform float s;
uniform vec3 w_camera_position;

in vec3 w_position, w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

vec4 fog_calc(vec4 shadedColor) {
    // Fog parameters
    float fog_maxdist = 500.0;
    float fog_mindist = 50;
    vec4 fog_colour = vec4(0.6, 0.6, 0.6, 1.0);
    
    // Calculate fog
    vec3 true_pos = (model * vec4(w_position,1)).xyz;
    float dist = length(true_pos - w_camera_position); 
    float fog_factor = (fog_maxdist - dist) / (fog_maxdist - fog_mindist);
    fog_factor = clamp(fog_factor, 0.0, 1.0);

    return mix(fog_colour, shadedColor, fog_factor);
}

void main() {
    //out_color = vec4(frag_tex_coords.x, frag_tex_coords.y, 0, 1);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, w_normal);
    
    vec3 tex_color = texture(diffuse_map, frag_tex_coords).rgb;
    vec3 diffuse_color = tex_color * max(dot(w_normal, l), .0);

    vec4 shadedColor = vec4(.7 * tex_color, 1) + vec4(diffuse_color, 1);

    out_color = fog_calc(shadedColor);
}
