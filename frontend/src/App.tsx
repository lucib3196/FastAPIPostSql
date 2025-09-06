import React, { useRef, useEffect, useState } from "react";
import AppOptions from "./components/AppOptions";
import CreateMonster from "./components/CreateMonster";
import ViewAllMonster from "./components/ViewAllMonsters";

import type { Option } from "./components/AppOptions";
import { ViewIndividualMonster } from "./components/ViewIndividualMonster";
export default function App() {
  const [option, setOption] = useState<Option>("View Single");

  return (
    <section className="min-h-screen w-full bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900 text-white">
      {/* Header / Hero */}
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
        <div className="text-center space-y-3 sm:space-y-4">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight">
            Monster PlayGround
          </h1>
          <p className="text-sm sm:text-base lg:text-lg text-gray-300">
            Create or view monsters — pick your mode below.
          </p>
        </div>

        {/* Options */}
        <div className="mt-6 sm:mt-8 flex justify-center">
          <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm shadow-lg p-3 sm:p-4">
            <AppOptions onChange={setOption} />
          </div>
        </div>

        {/* Main card */}
        <div className="mt-8 sm:mt-10">
          <div
            className="mx-auto flex justify-center max-w-6xl rounded-2xl border border-white/10 
                       bg-white/5 backdrop-blur-md shadow-2xl p-4 sm:p-6 lg:p-8
                       transition-all"
          >
            {option === "Create" ? (
              <CreateMonster />
            ) : option === "View Single" ? (
              <ViewIndividualMonster />
            ) : option === "View All Animations" ? (
              <ViewAllMonster />
            ) : null}
          </div>
        </div>
      </div>

      {/* Footer / subtle hint */}
      <div className="pb-10 text-center text-xs text-gray-400">
        tip: resize the window — layout adapts 🌊
      </div>
    </section>
  );
}
