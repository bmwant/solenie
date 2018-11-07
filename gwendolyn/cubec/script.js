//
// start here
//
var cubeRotation = 0.0;


function main() {
  const canvas = document.querySelector("#glCanvas");
  // Initialize the GL context
  const gl = canvas.getContext("webgl");
  const texture = loadTexture(gl, 'cubetexture.png');

  // Only continue if WebGL is available and working
  if (gl === null) {
    alert("Unable to initialize WebGL. Your browser or machine may not support it.");
    return;
  }

  // Set clear color to black, fully opaque
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  // Clear the color buffer with specified clear color
  gl.clear(gl.COLOR_BUFFER_BIT);

  const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec2 aTextureCoord;
    
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    
    varying highp vec2 vTextureCoord;
    
    void main() {
      gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
      vTextureCoord = aTextureCoord;
    }
  `;
  const fsSource = `
    varying highp vec2 vTextureCoord;
    
    uniform sampler2D uSampler;
    
    void main(void) {
      gl_FragColor = texture2D(uSampler, vTextureCoord);
    }
  `;
  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
      vertexColor: gl.getAttribLocation(shaderProgram, 'aVertexColor'),
      textureCoord: gl.getAttribLocation(shaderProgram, 'aTextureCoord'),
    },
    uniformLocations: {
      projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
      modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
      uSampler: gl.getUniformLocation(shaderProgram, 'uSampler'),
    },
  };
  const buffers = initBuffers(gl);
  var then = 0;

  function render(now) {
    now *= 0.001;
    const deltaTime = now - then;
    then = now;

    drawScene(gl, programInfo, buffers, texture, deltaTime);
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}


function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
    return null;
  }

  return shaderProgram;
}

function loadShader(gl, type, source) {
  const shader = gl.createShader(type);

  gl.shaderSource(shader, source);

  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

function initBuffers(gl) {
  const textureCoordBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, textureCoordBuffer);

  const textureCoordinates = [
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,

    // Back
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,

    // Top
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,

    // Bottom
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,

    // Right
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,

    // Left
    0.0,  0.0,
    1.0,  0.0,
    1.0,  1.0,
    0.0,  1.0,
  ];

  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(textureCoordinates),
    gl.STATIC_DRAW);

  const indexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  const indices = [
     0,  1,  2,    0,  2,  3,  // front
     4,  5,  6,    4,  6,  7,  // back
     8,  9, 10,    8, 10, 11,  // top
    12, 13, 14,   12, 14, 15,  // bottom
    16, 17, 18,   16, 18, 19,  // right
    20, 21, 22,   20, 22, 23,  // left
  ];
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
    new Uint16Array(indices), gl.STATIC_DRAW);



  const positionBuffer = gl.createBuffer();

  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  const positions = [
    // Front face
    -1.0, -1.0,  1.0,
     1.0, -1.0,  1.0,
     1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,

    // Back face
    -1.0, -1.0, -1.0,
    -1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0, -1.0, -1.0,

    // Top face
    -1.0,  1.0, -1.0,
    -1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0, -1.0,

    // Bottom face
    -1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0,  1.0,
    -1.0, -1.0,  1.0,

    // Right face
     1.0, -1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0,  1.0,
     1.0, -1.0,  1.0,

    // Left face
    -1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0,  1.0, -1.0,
  ];

  gl.bufferData(gl.ARRAY_BUFFER,
    new Float32Array(positions),
    gl.STATIC_DRAW);

  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
    new Uint16Array(indices), gl.STATIC_DRAW);

  return {
    position: positionBuffer,
    textureCoord: textureCoordBuffer,
    indices: indexBuffer,
  }
}


function drawScene(gl, programInfo, buffers, texture, deltaTime) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  gl.clearDepth(1.0);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LEQUAL);

  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  const fieldOfView = 45 * Math.PI / 180;
  const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
  const zNear = 0.1;
  const zFar = 100.0;
  const projectionMatrix = mat4.create();

  mat4.perspective(projectionMatrix,
    fieldOfView,
    aspect,
    zNear,
    zFar);

  const modelViewMatrix = mat4.create();

  mat4.translate(modelViewMatrix,
    modelViewMatrix,
    [-0.0, 0.0, -6.0]);

  mat4.rotate(
    modelViewMatrix,
    modelViewMatrix,
    cubeRotation * 0.8,
    [0, 0, 1]
  );

  mat4.rotate(
    modelViewMatrix,  // destination matrix
    modelViewMatrix,  // matrix to rotate
    cubeRotation * 0.7,  // amount to rotate in radians
    [0, 1, 0]
  );  // axis to rotate around

  mat4.rotate(
    modelViewMatrix,  // destination matrix
    modelViewMatrix,  // matrix to rotate
    cubeRotation * 0.2,  // amount to rotate in radians
    [1, 0, 0]
  );  // axis to rotate around

  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);

  {
    const vertexCount = 36;
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
  }

  {
    const num = 2;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.textureCoord);
    gl.vertexAttribPointer(programInfo.attribLocations.textureCoord, num, type,
      normalize, stride, offset);
    gl.enableVertexAttribArray(programInfo.attribLocations.textureCoord);
  }
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.uniform1i(programInfo.uniformLocations.uSampler, 0);

  {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(
      programInfo.attribLocations.vertexPosition,
      numComponents,
      type,
      normalize,
      stride,
      offset
    );
    gl.enableVertexAttribArray(
      programInfo.attribLocations.vertexPosition
    );
  }

  gl.useProgram(programInfo.program);

  gl.uniformMatrix4fv(
    programInfo.uniformLocations.projectionMatrix,
    false,
    projectionMatrix
  );
  gl.uniformMatrix4fv(
    programInfo.uniformLocations.modelViewMatrix,
    false,
    modelViewMatrix
  );

  {
    const offset = 0;
    const vertexCount = 4;
    gl.drawArrays(gl.TRIANGLE_STRIP, offset, vertexCount);
  }

  cubeRotation += deltaTime;
}
