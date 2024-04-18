#version 330 core

uniform sampler2D texture_map;
uniform float alpha;

// receiving interpolated color for fragment shader
in vec2 frag_tex_coords;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    //out_color = texture(texture_map, frag_tex_coords);
    //out_color = vec4(out_color.r, out_color.g, out_color.b, alpha);
    out_color = vec4(frag_tex_coords, 1, alpha);
}
