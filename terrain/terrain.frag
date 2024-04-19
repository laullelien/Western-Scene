#version 330 core

in vec3 w_position, w_normal;

uniform vec3 light_dir;

uniform vec3 k_a, k_d, k_s;
uniform float s;

uniform vec3 w_camera_position;

uniform sampler2D diffuse_map;

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
    // Compute all vectors, oriented outwards from the fragment
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, w_normal);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 tex_color = vec3(texture(diffuse_map, w_position.xy / 30.0));
    vec3 diffuse_color = tex_color * max(dot(w_normal, l), .0);
    vec3 specular_color = k_s * pow(max(dot(r, v), .0), s);

    vec4 shadedColor = vec4(.7 * tex_color, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);

    out_color = fog_calc(shadedColor);
}
