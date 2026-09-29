-- NonEKI replaces the eating radio with a blank animation at 0.1 chars/s.
-- Korean translations restore its text, so restore the normal typing speed.
function patch(config)
  if config.full and config.full.textSpeed == 0.1 then
    config.full.textSpeed = 40
  end

  -- NonEKI's FU branch removes this message even though the cave still calls it.
  if config.naturalcave1 and not config.naturalcave2 then
    config.naturalcave2 = {
      type = config.naturalcave1.type or "tutorial",
      text = "개인 전투 능력에 자신이 없다면, 들어가기 전에 더 좋은 장비를 만드는 것이 더 적합할 것입니다.",
      textSpeed = 40,
      portraitImage = config.naturalcave1.portraitImage,
      portraitFrames = config.naturalcave1.portraitFrames,
      portraitSpeed = config.naturalcave1.portraitSpeed,
      persistTime = 10
    }
  end
  return config
end
