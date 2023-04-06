#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;

float randomHeight(vec3 position, float maxHeight){
    float height = sqrt(pow(position.x,2) + pow(position.z,2));
    if(height < maxHeight-2)
        return mod(height,maxHeight)-1;
    if(height < maxHeight*2)
        return maxHeight-height;
    // else
        // return maxHeight-mod(height,maxHeight);
    return -100.0;
}

void main() {
    // initialize interpolated colors at vertices
    fragment_color = color;
    float maxHeight = 4.5;

    // tell OpenGL how to transform the vertex to clip coordinates
    float newHeight = randomHeight(position, maxHeight);
    vec3 newPos;
    if(newHeight == -100)
        newPos = vec3(0,-maxHeight,0);
    else
        newPos = vec3(position.x, newHeight, position.z);

    gl_Position = projection * view * vec4(newPos, 1);
}
