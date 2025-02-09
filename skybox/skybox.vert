#version 330 core
in vec3 aPos;

out vec3 TexCoords;

uniform mat4 projection;
uniform mat4 view;

void main()
{
    TexCoords = aPos;
    // disable translations
    mat4 skyboxView = mat4(mat3(view));

    vec4 pos = projection * skyboxView * vec4(aPos, 1.0);
    gl_Position = pos.xyww;
} 