import { MyButton } from "./MyButton";

export type Option = "Create" | "View";

type AppOptionsProps = {
    value: Option; // current selection from parent
    onChange: (next: Option) => void; // notify parent
};

export default function AppOptions({ value, onChange }: AppOptionsProps) {
    return (
        <div className="flex flex-row justify-center gap-x-5">
            <MyButton
                variant={"secondary"}
                name={"Create A Monster"}

                onClick={() => onChange("Create")}
            ></MyButton>
            <MyButton
                name={"View the Monsters"}
                onClick={() => onChange("View")}
                
            ></MyButton>
        </div>
    );
}