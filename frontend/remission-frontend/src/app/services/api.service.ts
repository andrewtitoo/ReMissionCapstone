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
   * Logs symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.)
   * @returns Observable for API response
   */
  logSymptoms(symptomData: any): Observable<any> {
    const url = `${this.baseUrl}/log-symptoms`;
    return this.http.post(url, symptomData, { headers: this.headers }).pipe(
      catchError(this.handleError('logging symptoms'))
    );
  }

  /**
   * Retrieves all logged symptoms for the current user.
   * @returns Observable for logged symptom data
   */
  getSymptomLogs(): Observable<any> {
    const url = `${this.baseUrl}/symptom-logs`;
    return this.http.get(url, { headers: this.headers }).pipe(
      catchError(this.handleError('fetching symptom logs'))
    );
  }

  /**
   * Fetches trend analysis insights from CHIIP.
   * @param userId The ID of the user to analyze logs for
   * @returns Observable for bot analysis response
   */
  getBotAnalysis(userId: number): Observable<any> {
    const url = `${this.baseUrl}/bot-analysis`;
    return this.http.post(url, { user_id: userId }, { headers: this.headers }).pipe(
      catchError(this.handleError('fetching bot analysis'))
    );
  }

  /**
   * Sends a user message to CHIIP and retrieves a response.
   * @param userMessage The message from the user to the bot
   * @returns Observable with the bot's response
   */
  getBotResponse(userMessage: string): Observable<any> {
    const url = `${this.baseUrl}/bot-response`;
    return this.http.post(url, { message: userMessage }, { headers: this.headers }).pipe(
      catchError(this.handleError('sending bot message'))
    );
  }

  /**
   * Generic error handler for API requests.
   * @param operation Description of the failed operation
   * @returns Observable that throws an error
   */
  private handleError(operation: string) {
    return (error: any): Observable<never> => {
      console.error(`Error during ${operation}:`, error); // Log to console for debugging
      alert(`An error occurred while ${operation}. Please try again later.`);
      return throwError(() => new Error('Something went wrong with the network request.'));
    };
  }
}

