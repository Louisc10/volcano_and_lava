#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float global_color;

in vec3 position;
in vec2 tex_coord;
in vec3 normal;

out vec2 frag_tex_coords;
out float frag_global_color;
out vec3 w_position;
out vec3 w_normal; 

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    frag_tex_coords = vec2(tex_coord.x * global_color, tex_coord.y * global_color) ;

    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model *vec4(position, 1)).xyz;
}