import { Separator } from "@/components/ui/separator";
import { ProfileForm } from "@/app/settings/profile-form";

export default function SettingsProfilePage() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">Settings</h3>
        <p className="text-sm text-muted-foreground">
          Change user settings.
        </p>
      </div>
      <Separator />
      <ProfileForm />
    </div>
  );
}
