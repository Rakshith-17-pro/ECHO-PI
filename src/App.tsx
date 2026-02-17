import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SOS from "./pages/SOS";
import Wiki from "./pages/Wiki";
import MapView from "./pages/MapView";
import Chat from "./pages/Chat";
import Translator from "./pages/Translator";
import Guides from "./pages/Guides";
import AdminLogin from "./pages/admin/AdminLogin";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminAlerts from "./pages/admin/AdminAlerts";
import AdminLogs from "./pages/admin/AdminLogs";
import AdminNodes from "./pages/admin/AdminNodes";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/sos" element={<SOS />} />
          <Route path="/wiki" element={<Wiki />} />
          <Route path="/map" element={<MapView />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/translator" element={<Translator />} />
          <Route path="/guides" element={<Guides />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/alerts" element={<AdminAlerts />} />
          <Route path="/admin/logs" element={<AdminLogs />} />
          <Route path="/admin/nodes" element={<AdminNodes />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
