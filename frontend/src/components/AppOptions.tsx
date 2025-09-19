import { MyButton } from "./MyButton";

export type Option = "Create" | "View Single" | "View All Animations";

type AppOptionsProps = {
  onChange: (next: Option) => void; // notify parent
};

export default function AppOptions({ onChange }: AppOptionsProps) {
  return (
    <div className="flex flex-row justify-center gap-x-5">
      <MyButton
        variant={"secondary"}
        name={"Create A Monster (coming soon)"}
 
        onClick={() => onChange("Create")}
      ></MyButton>
      <MyButton
        name={"View the Monster (Beta)"}
        onClick={() => onChange("View Single")}
      ></MyButton>
      <MyButton
        variant={"success"}
        name={"View all Animations (Beta)"}
        onClick={() => onChange("View All Animations")}
      ></MyButton>
    </div>
  );
}
