import { LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";
import { Card } from "@/components/ui/card";

interface FeatureCardProps {
  title: string;
  icon: LucideIcon;
  href: string;
  color?: "primary" | "accent" | "secondary";
}

export const FeatureCard = ({ title, icon: Icon, href, color = "primary" }: FeatureCardProps) => {
  const colorClasses = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90",
    accent: "bg-accent text-accent-foreground hover:bg-accent/90",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/90",
  };

  return (
    <Link to={href}>
      <Card className={`p-6 transition-all hover:scale-105 hover:shadow-lg ${colorClasses[color]} border-0`}>
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="rounded-full bg-white/20 p-4">
            <Icon className="h-8 w-8" />
          </div>
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
      </Card>
    </Link>
  );
};
