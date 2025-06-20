    def draw_how_to_play(self):
        """Recreated How to Play screen with better spacing and layout"""
        self.screen.fill((15, 25, 45))  # Dark blue background
        
        # Title with more space from top
        title_text = self.font_large.render("HOW TO PLAY", True, WHITE)
        title_rect = title_text.get_rect(center=(GAME_AREA_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # VEHICLES section - better positioned
        vehicles_y = 180
        vehicles_title = self.font_medium.render("VEHICLES", True, YELLOW)
        vehicles_rect = vehicles_title.get_rect(center=(GAME_AREA_WIDTH // 2, vehicles_y))
        self.screen.blit(vehicles_title, vehicles_rect)
        
        # Sprite display area - more spread out across wider screen
        sprite_y = vehicles_y + 80
        sprite_names = ['player_car', 'enemy_static', 'enemy_police', 'enemy_sports']
        # Better spacing for 1200px width
        x_positions = [200, 350, 500, 650, 800, 950]
        
        # Display first 4 sprites (cars)
        for i, sprite_name in enumerate(sprite_names):
            if i < 4:  # Only first 4 positions for cars
                sprite = self.sprite_manager.get_sprite(sprite_name)
                if sprite:
                    sprite_rect = sprite.get_rect(center=(x_positions[i], sprite_y))
                    self.screen.blit(sprite, sprite_rect)
        
        # Vehicle labels - clearer spacing
        labels = ["PLAYER", "ENEMY", "POLICE", "SPORTS"]
        descriptions = ["YOU", "BASIC", "DODGES", "ZIGZAG"]
        
        for i, (label, desc) in enumerate(zip(labels, descriptions)):
            if i < 4:
                # Main label
                label_text = self.font_small.render(label, True, WHITE)
                label_rect = label_text.get_rect(center=(x_positions[i], sprite_y + 70))
                self.screen.blit(label_text, label_rect)
                
                # Description
                desc_text = self.font_tiny.render(desc, True, GRAY)
                desc_rect = desc_text.get_rect(center=(x_positions[i], sprite_y + 95))
                self.screen.blit(desc_text, desc_rect)
        
        # FUEL section - separate and clear
        fuel_y = sprite_y + 160
        fuel_title = self.font_medium.render("FUEL STATION", True, GREEN)
        fuel_title_rect = fuel_title.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y))
        self.screen.blit(fuel_title, fuel_title_rect)
        
        # Fuel station sprite - centered
        fuel_sprite = self.sprite_manager.get_sprite('fuel_station')
        if fuel_sprite:
            fuel_rect = fuel_sprite.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y + 70))
            self.screen.blit(fuel_sprite, fuel_rect)
        
        # Fuel description
        fuel_desc = self.font_small.render("COLLECT TO REFUEL", True, GREEN)
        fuel_desc_rect = fuel_desc.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y + 140))
        self.screen.blit(fuel_desc, fuel_desc_rect)
        
        # CONTROLS and OBJECTIVE sections - side by side with more space
        bottom_y = fuel_y + 200
        
        # CONTROLS section - left side
        controls_x = 250
        controls_title = self.font_medium.render("CONTROLS", True, YELLOW)
        self.screen.blit(controls_title, (controls_x, bottom_y))
        
        controls = [
            "ARROW KEYS - MOVE CAR",
            "ESC - RETURN TO MENU", 
            "F11 - FULLSCREEN"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_tiny.render(control, True, WHITE)
            self.screen.blit(control_text, (controls_x, bottom_y + 40 + (i * 30)))
        
        # OBJECTIVE section - right side
        objective_x = 700
        objective_title = self.font_medium.render("OBJECTIVE", True, RED)
        self.screen.blit(objective_title, (objective_x, bottom_y))
        
        objectives = [
            "AVOID ENEMY CARS",
            "COLLECT FUEL TO SURVIVE",
            "DRIVE AS FAR AS POSSIBLE"
        ]
        
        for i, objective in enumerate(objectives):
            obj_text = self.font_tiny.render(objective, True, WHITE)
            self.screen.blit(obj_text, (objective_x, bottom_y + 40 + (i * 30)))
        
        # Instructions at bottom - more space
        instruction_y = SCREEN_HEIGHT - 100
        instruction_text = self.font_small.render("PRESS SPACE TO START GAME", True, YELLOW)
        instruction_rect = instruction_text.get_rect(center=(GAME_AREA_WIDTH // 2, instruction_y))
        self.screen.blit(instruction_text, instruction_rect)
        
        escape_text = self.font_tiny.render("PRESS ESC TO RETURN TO MENU", True, GRAY)
        escape_rect = escape_text.get_rect(center=(GAME_AREA_WIDTH // 2, instruction_y + 40))
        self.screen.blit(escape_text, escape_rect)
