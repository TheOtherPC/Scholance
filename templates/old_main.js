const canvas = document.getElementById("canvas");
const c = canvas.getContext("2d");

// size of canvas
const imgSize = 512;

canvas.width = imgSize;
canvas.height = imgSize;

// init image data with black pixels
const image = c.createImageData(imgSize, imgSize);
for (let i = 0; i < image.data.length; i += 4) {
  image.data[i] = 0; // R
  image.data[i + 1] = 0; // G
  image.data[i + 2] = 0; // B
  image.data[i + 3] = 255; // A
}

// size of our height maps
const mapSize = 1024;
// distance formula
const distance = (x, y) => Math.sqrt(x * x + y * y);

// init height map 1
const heightMap1 = [];
for (let u = 0; u < mapSize; u++) {
  for (let v = 0; v < mapSize; v++) {

    const i = u * mapSize + v;

    const cx = u - mapSize / 2;
    const cy = v - mapSize / 2;

    const d = distance(cx, cy);
    const stretch = (3 * Math.PI) / (mapSize / 2);
    const ripple = Math.sin(d * stretch);
    const normalized = (ripple + 1) / 2;

    heightMap1[i] = Math.floor(normalized * 128);
  }
}

const heightMap2 = [];
for (let u = 0; u < mapSize; u++) {
  for (let v = 0; v < mapSize; v++) {
    const i = u * mapSize + v;
    const cx = u - mapSize / 2;
    const cy = v - mapSize / 2;

    const d1 = distance(0.8 * cx, 1.3 * cy) * 0.022;
    const d2 = distance(1.35 * cx, 0.45 * cy) * 0.022;

    const s = Math.sin(d1);
    const c = Math.cos(d2);
    const h = s + c;

    const normalized = (h + 2) / 4;

    heightMap2[i] = Math.floor(normalized * 128);
  }
}

let palettes = Array(64).fill({ r: 202, g: 172, b: 123 }).concat(Array(192).fill({ r: 255, g: 255, b: 255 }));

const updateImageData = () => {
  for (let u = 0; u < imgSize; u++) {
    for (let v = 0; v < imgSize; v++) {
      // indexes into height maps for pixel
      const i = u * mapSize + v;
      // index for pixel in image data
      // remember it's 4 bytes per pixel
      const p = u * imgSize * 4 + v * 4;

      // height value of 0..255
      let h = heightMap1[i] + heightMap2[i];
      // get color value from current palette
      let c = palettes[h];

      // set pixel data
      image.data[p] = c.r;
      image.data[p + 1] = c.g;
      image.data[p + 2] = c.b;
    }
  }
};

updateImageData();
c.putImageData(image, 0, 0);