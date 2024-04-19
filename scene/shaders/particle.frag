#version 330 core

uniform sampler2D texture_map;
uniform float alpha;

// receiving interpolated color for fragment shader
in vec2 frag_tex_coords;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    float x = frag_tex_coords.x - 0.5;
    float y = frag_tex_coords.y - 0.5;
    float dist = sqrt((x * x) + (y * y));
    
    if(dist <= 0.3)
        out_color = vec4(0.5, 0.5, 0.5, alpha);
    else
        discard;

    //out_color = vec4(frag_tex_coords, 1, alpha);
}
