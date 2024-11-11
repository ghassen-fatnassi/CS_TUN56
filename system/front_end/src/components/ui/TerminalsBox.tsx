import { useDrawerContext } from "./DrawerContext";
import Terminal from "./Terminal";
import "../../styles.css";

export default function TerminalsBox() {
  const { attackerAction, defenderAction } = useDrawerContext();

  return (
    <div className="terminal-box">
      <Terminal
        bgColor={"#661b1c"}
        promptColor="red"
        prompt={`Attacker Action: ${attackerAction || "No Action"}`}
      />
      <Terminal
        bgColor={"#235347"}
        promptColor="white"
        prompt={`Defender Action: ${defenderAction || "No Action"}`}
      />
    </div>
  );
}
