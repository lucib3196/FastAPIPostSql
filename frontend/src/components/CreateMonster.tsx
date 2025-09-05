export default function CreateMonster() {
    return (
        <div className="w-full flex flex-col justify-center items-centerw-full text-white px-6 py-8 bg-gray-900 rounded-2xl">
            <h1 className="font-bold text-3xl text-center mb-8">
                Create Your Own Monster!
            </h1>

            <form action="submit" className="space-y-10">
                {/* Identity Section */}
                <section className="flex flex-col space-y-4">
                    <h2 className="text-2xl font-bold">Identity</h2>
                    <hr className="border-gray-500" />

                    <label
                        htmlFor="MonsterName"
                        className="block text-sm font-bold"
                    >
                        Monster Name
                    </label>
                    <input
                        type="text"
                        id="MonsterName"
                        placeholder="e.g. Fluffernox"
                        className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-50 text-black leading-tight focus:outline-none focus:shadow-outline"
                    />

                    <label
                        htmlFor="Description"
                        className="block text-sm font-bold"
                    >
                        Short Description
                    </label>
                    <textarea
                        id="Description"
                        rows={4}
                        placeholder="A playful cloud fox that loves mountain skies..."
                        className="shadow appearance-none border rounded w-full py-2 px-3  bg-gray-50 text-black leading-tight focus:outline-none focus:shadow-outline"
                    />
                </section>

                {/* Visual Appearance Section */}
                <section className="flex flex-col space-y-4">
                    <h2 className="text-2xl font-bold">Visual Appearance</h2>
                    <hr className="border-gray-500" />

                    <label
                        htmlFor="MonsterPhysical"
                        className="block text-sm font-bold"
                    >
                        Physical Features
                    </label>
                    <textarea
                        id="MonsterPhysical"
                        rows={4}
                        placeholder="Describe body shape, colors, wings, horns, etc."
                        className="shadow appearance-none border rounded w-full py-2 px-3  bg-gray-50 text-black leading-tight focus:outline-none focus:shadow-outline"
                    />
                </section>

                {/* Attributes Section */}
                <section className="flex flex-col space-y-4">
                    <h2 className="text-2xl font-bold">Attributes</h2>
                    <hr className="border-gray-500" />

                    <div className="space-y-2">
                        {["fire", "water", "grass", "electric", "psychic"].map((val) => (
                            <label key={val} className="flex items-center gap-x-2">
                                <input type="radio" name="type" value={val} />
                                {val.charAt(0).toUpperCase() + val.slice(1)}
                            </label>
                        ))}
                    </div>
                </section>
            </form>
        </div>
    );
}