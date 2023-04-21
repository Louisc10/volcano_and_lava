#version 330 core

uniform sampler2D diffuse_map;

// light dir, in world coordinates
// uniform vec3 light_dir;

// material properties
uniform vec3 k_a;
// uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

in vec3 w_position;
in vec3 w_normal;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    vec3 k_d = texture(diffuse_map, frag_tex_coords).rgb;

    out_color =  vec4(k_d, 1);

    // //One texture
    // out_color = texture(diffuse_map, frag_tex_coords);

    // // two texture
    // vec4 color1 = texture(diffuse_map, frag_tex_coords);
    // vec4 color2 = texture(second_texture, frag_tex_coords);
    // out_color = mix(color1, color2, color2.a);  // analyse what is done here!
}