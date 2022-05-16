command SerenadeStart call serenade#Init()
command SerenadeActive call serenade#Active()

if get(g:, 'serenade_autostart', 1)
    SerenadeStart
end
