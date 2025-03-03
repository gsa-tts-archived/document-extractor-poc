import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "@uswds/uswds/dist/css/uswds.min.css"
import "@uswds/uswds/dist/js/uswds.min.js"
import "./css/styles.css"

const container = document.getElementById("app");
const root = createRoot(container)
root.render(<App />);