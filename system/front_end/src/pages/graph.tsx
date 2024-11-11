import Architecture from "../components/ui/Architecture";
import TerminalDrawer from "../components/ui/TerminalDrawer";
import { DrawerProvider } from "../components/ui/DrawerContext";

export default function Graph() {
    return (
        <>
            <DrawerProvider>
                <Architecture />
                {/*<TerminalsBox />*/}
                <TerminalDrawer />
            </DrawerProvider>
        </>
    );
}