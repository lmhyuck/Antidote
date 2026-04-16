import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/global.css";
import App from "../src/App";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// 지우면 안 됩니다.
// React 앱의 시작점(진입점)이라서
// 이 파일이 없으면 앱 자체가 실행 안 됩니다.
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
