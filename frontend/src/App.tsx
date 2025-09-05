
import { useState } from "react";
import AppOptions from "./components/AppOptions";
import CreateMonster from "./components/CreateMonster";
import type { Option } from "./components/AppOptions";

function App() {
  const [option, setOption] = useState<Option>("Create");
  return (
    <section className="w-full h-full flex flex-col items-center space-y-10 bg-gray-800">
      <div className="flex flex-col justify-center items-center mx-auto my-40 gap-y-5">
        <h1 className="font-bold text-2xl text-white">Monster PlayGround</h1>
        <p className="font-bold text-gray-300">Create or View Monsters</p>
        <AppOptions value={option} onChange={setOption} />
      </div>
      <div className="flex flex-col w-7/10  items-center justify-center m-6 gap-y-4">

        {option === "Create" ? <CreateMonster /> : <ViewMonsters />}
      </div>
    </section>
  );
}



function ViewMonsters() {
  return <div className="text-white">A collection of Monsters</div>;
}

export default App;
