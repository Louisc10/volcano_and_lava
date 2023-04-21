#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 position;
in vec2 tex_coord;
in vec3 normal;

out vec2 frag_tex_coords;
out vec3 w_position;
out vec3 w_normal; 

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    frag_tex_coords = tex_coord;

    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model *vec4(position, 1)).xyz;
}