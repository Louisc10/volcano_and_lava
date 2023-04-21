#version 330 core

uniform float global_color;
uniform sampler2D diffuse_map;

in vec3 w_position;
in vec3 w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    vec3 tint = vec3(global_color, global_color, 0);
    vec3 k_d = texture(diffuse_map, frag_tex_coords).rgb + tint;

    out_color =  vec4(k_d, 1);
}