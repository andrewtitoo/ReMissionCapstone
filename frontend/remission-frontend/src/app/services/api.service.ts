import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  /**
   * Logs symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.)
   * @returns Observable for API response
   */
  logSymptoms(symptomData: any): Observable<any> {
    const url = `${this.baseUrl}/log-symptoms`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post(url, symptomData, { headers });
  }

  /**
   * Retrieves all logged symptoms for the current user.
   * @returns Observable for logged symptom data
   */
  getSymptomLogs(): Observable<any> {
    const url = `${this.baseUrl}/symptom-logs`;
    return this.http.get(url);
  }

  /**
   * Fetches trend analysis insights from CHIIP.
   * @returns Observable for bot analysis response
   */
  getBotAnalysis(): Observable<any> {
    const url = `${this.baseUrl}/bot-analysis`;
    return this.http.get(url);
  }

  /**
   * Sends a user message to CHIIP and retrieves a response.
   * @param userMessage The message from the user to the bot
   * @returns Observable with the bot's response
   */
  getBotResponse(userMessage: string): Observable<any> {
    const url = `${this.baseUrl}/bot-response`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post(url, { message: userMessage }, { headers });
  }
}
