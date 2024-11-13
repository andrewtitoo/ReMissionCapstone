import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root' // Ensures the service is available application-wide
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api'; // Base URL for your API
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  /**
   * Automatically assigns a new User ID.
   * @returns Observable containing the assigned User ID.
   */
  autoAssignUser(): Observable<{ user_id: string }> {
    const url = `${this.baseUrl}/auto-assign-user`;
    return this.http.post<{ user_id: string }>(url, {}, { headers: this.headers }).pipe(
      catchError(this.handleError('auto-assigning a user ID'))
    );
  }

  /**
   * Logs symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.).
   * @returns Observable for API response.
   */
  logSymptoms(symptomData: any): Observable<{ message: string }> {
    const url = `${this.baseUrl}/log-symptoms`;
    return this.http.post<{ message: string }>(url, symptomData, { headers: this.headers }).pipe(
      catchError(this.handleError('logging symptoms'))
    );
  }

  /**
   * Retrieves all logged symptoms for the specified user.
   * @param userId The ID of the user to retrieve logs for.
   * @returns Observable for logged symptom data.
   */
  getSymptomLogs(userId: string): Observable<SymptomLog[]> {
    const url = `${this.baseUrl}/symptom-logs?user_id=${userId}`;
    return this.http.get<SymptomLog[]>(url, { headers: this.headers }).pipe(
      catchError((error) => {
        console.error('API Error [getSymptomLogs]:', error); // Log detailed error for debugging
        return throwError(() => new Error(`Failed to fetch symptom logs: ${error.message || error}`));
      })
    );
  }

  /**
   * Fetches insights from CHIIP based on user symptom logs.
   * @param userId The ID of the user to analyze logs for.
   * @returns Observable for bot analysis response.
   */
  getBotAnalysis(userId: string): Observable<{ classification: string; insights: string[] }> {
    const url = `${this.baseUrl}/bot-analysis`;
    const payload = { user_id: userId };
    return this.http.post<{ classification: string; insights: string[] }>(url, payload, { headers: this.headers }).pipe(
      catchError(this.handleError('fetching bot analysis'))
    );
  }

  /**
   * Sends a user message to CHIIP and retrieves a response.
   * @param userMessage The message from the user to the bot.
   * @returns Observable with the bot's response.
   */
  getBotResponse(userMessage: string): Observable<{ response: string }> {
    const url = `${this.baseUrl}/bot-response`;
    const payload = { message: userMessage };
    return this.http.post<{ response: string }>(url, payload, { headers: this.headers }).pipe(
      catchError(this.handleError('sending a bot message'))
    );
  }

  /**
   * Validates if a given User ID exists in the system.
   * @param userId The User ID to validate.
   * @returns Observable for API response.
   */
  validateUserId(userId: string): Observable<{ message: string }> {
    const url = `${this.baseUrl}/auto-assign-user`; // Adjust if your endpoint differs
    return this.http.post<{ message: string }>(url, { user_id: userId }, { headers: this.headers }).pipe(
      catchError(this.handleError('validating the user ID'))
    );
  }

  /**
   * Generic error handler for API requests.
   * @param operation Description of the failed operation.
   * @returns Observable that throws an error.
   */
  private handleError(operation: string) {
    return (error: any): Observable<never> => {
      console.error(`Error during ${operation}:`, error); // Log to console for debugging
      const errorMessage = error.error?.message || `An error occurred while ${operation}. Please try again later.`;
      alert(errorMessage);
      return throwError(() => new Error(errorMessage));
    };
  }
}

/**
 * Interface to describe symptom log data structure.
 */
interface SymptomLog {
  logged_at: string;
  pain_level: number;
  stress_level: number;
  sleep_hours: number;
  exercise_done?: boolean;
  exercise_type?: string[];
  took_medication?: boolean;
  flare_up?: number;
}
