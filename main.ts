import { mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const bytes = readFileSync(new URL("./entry.png", import.meta.url));
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png does not start with the PNG signature");
}
if (bytes.subarray(12, 16).toString("latin1") !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk where one is expected");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const target = join(outDir, "entry.png");
const tmp = join(outDir, `.entry.png.${process.pid}.tmp`);
writeFileSync(tmp, bytes);
renameSync(tmp, target);
console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
