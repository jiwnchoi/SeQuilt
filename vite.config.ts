import anywidget from "@anywidget/vite";
import { UserConfig, defineConfig } from "vite";
import config from "./vite.config.json";

export default defineConfig({
	...(config as Partial<UserConfig>),
	plugins: [anywidget()],
});
