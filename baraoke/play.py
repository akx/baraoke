import re

import pygame

from baraoke.job import Job

HEIGHT = 720

WIDTH = 1280


def play(job: Job):

    whisper_data = job.read_whisper_json()
    silence_data = job.read_silence_infos_json()
    initial_silence = None
    if silence_data:
        silence_data_iter = iter(silence_data)
        assert next(silence_data_iter)[0] == "start"
        initial_silence_pair = next(silence_data_iter)
        assert initial_silence_pair[0] == "end"
        initial_silence = initial_silence_pair[1]

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.SysFont("Helvetica", 30)
    pygame.mixer.music.load(job.remuxed_low_vox_path)
    music_start_offset = 20
    pygame.mixer.music.play(start=music_start_offset)

    print(initial_silence)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        screen.fill("purple")

        music_pos_sec = pygame.mixer.music.get_pos() / 1000.0 + music_start_offset

        for transcript in whisper_data.transcription:
            start_time_sec = transcript.offsets.from_ / 1000.0  # - initial_silence
            end_time_sec = transcript.offsets.to / 1000.0  # - initial_silence
            dur = (end_time_sec - start_time_sec)
            if dur <= 0.05:
                continue
            progress = (music_pos_sec - start_time_sec) / dur
            y_off = (start_time_sec - music_pos_sec) * 25

            tx = re.sub(r"\[.+?\]", "", transcript.text)
            text = font.render(tx, 1, [255, 255, 255])
            rect = text.get_rect()

            rect.center = (WIDTH / 2.0, HEIGHT / 2.0 + y_off)
            screen.blit(text, rect)

            if 0 <= progress <= 1:
                text = font.render(tx, 1, [255, 0, 0])
                rect = text.get_rect()
                rect.center = (WIDTH / 2.0, HEIGHT / 2.0 + y_off)
                screen.blit(text, rect, area=(0, 0, progress * rect.width, rect.height))

        text = font.render(f"{music_pos_sec:.2f}", 1, [255, 255, 255])
        rect = text.get_rect()
        screen.blit(text, rect)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
