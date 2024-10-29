import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-logger',
  templateUrl: './logger.component.html',
  standalone: true,
  styleUrls: ['./logger.component.css'],
  imports: [FormsModule]  // Make sure FormsModule is included here
})
export class LoggerComponent {
  // Form fields
  painLevel: number = 5;
  stressLevel: number = 5;
  sleepHours: number = 7;
  exerciseDone: boolean = false;
  tookMedication: boolean = false;

  // Exercise types
  exerciseTypes = [
    { name: 'Cardio', selected: false },
    { name: 'Strength', selected: false },
    { name: 'Yoga', selected: false },
    { name: 'Walking', selected: false }
  ];

  constructor(private apiService: ApiService) {}

  onSubmit(): void {
    const loggedData = {
      pain_level: this.painLevel,
      stress_level: this.stressLevel,
      sleep_hours: this.sleepHours,
      exercise_done: this.exerciseDone,
      exercise_types: this.exerciseTypes.filter(e => e.selected).map(e => e.name),
      took_medication: this.tookMedication
    };

    // Send data to backend via ApiService
    this.apiService.logSymptoms(loggedData).subscribe(
      () => {
        alert('Your symptoms have been logged successfully!');
      },
      (error: any) => {  // Fix for TS7006: Explicitly specifying the type of `error`
        console.error('Error logging symptoms:', error);
        alert('An error occurred while logging your symptoms. Please try again later.');
      }
    );
  }

  getProgress(): number {
    let progress = 0;
    if (this.painLevel > 0) progress += 20;
    if (this.stressLevel > 0) progress += 20;
    if (this.sleepHours > 0) progress += 20;
    if (this.exerciseDone) progress += 20;
    if (this.tookMedication) progress += 20;
    return progress;
  }
}
