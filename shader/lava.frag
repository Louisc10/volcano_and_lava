#version 330 core

uniform sampler2D diffuse_map;
uniform float global_color;

in vec3 w_position;
in vec3 w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    vec3 k_d = texture(diffuse_map, frag_tex_coords).rgb * global_color *10;

    out_color =  vec4(k_d, 1);
}