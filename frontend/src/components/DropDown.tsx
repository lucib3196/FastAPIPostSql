type DropDownProps = {
    animations: string[];
    selectedAnimation: string;
    onChange: (e: string) => void;
};
export function Dropdown({
    animations,
    selectedAnimation,
    onChange,
}: DropDownProps) {
    return (
        <select
            value={selectedAnimation}
            onChange={(e) => onChange(e.target.value)}
            className="w-full my-3 bottom-0 px-3 py-2 rounded-lg border border-gray-300 bg-white shadow-sm
                 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                 text-gray-700 cursor-pointer"
        >
            {/* Optional placeholder when nothing selected yet */}
            {selectedAnimation === "" && (
                <option value="" disabled>
                    Select animation…
                </option>
            )}
            {animations.map((anim) => (
                <option key={anim} value={anim} className="text-gray-700">
                    {anim.toUpperCase()}
                </option>
            ))}
        </select>
    );
}