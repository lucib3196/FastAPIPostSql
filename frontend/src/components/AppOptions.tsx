import { MyButton } from "./MyButton";

export type Option = "Create" | "View";

type AppOptionsProps = {
    onChange: (next: Option) => void; // notify parent
};

export default function AppOptions({ onChange }: AppOptionsProps) {
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