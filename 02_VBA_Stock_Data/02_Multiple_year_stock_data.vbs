Attribute VB_Name = "Module1"
Sub CalculateVolumeByTicker()

Dim Ticker As String
Dim DailyVolume As Double
Dim TickerVolumeSubtotal As Double
Dim LastTickerRow As Long
Dim TickerSubtotalRow As Integer
Dim RowsProcessed As Integer

Dim YearOpen As Double
Dim YearClose As Double
Dim YearlyChange As Double
Dim YearlyPercentChange As Double

Dim TickerWithGreatestIncrease As String
Dim TickerWithGreatestDecrease As String
Dim TickerWithGreatestVolume As String
Dim GreatestIncrease As Double
Dim GreatestDecrease As Double
Dim GreatestVolume As Double

Dim ws As Worksheet

For Each ws In ActiveWorkbook.Worksheets

'Initialize everything for processing the current sheet
RowsProcessed = 0 'Initialize rows processed. Used to count how many tickers are in a group which will help find the first one.
TickerSubtotalRow = 2 'Row to start the subtotal
LastTickerRow = ws.Range("A1").CurrentRegion.Rows.Count 'Count how many rows of tickers to use in loop
TickerWithGreatestIncrease = ""
TickerWithGreatestDecrease = ""
TickerWithGreatestVolume = ""
GreatestIncrease = 0
GreatestDecrease = 0
GreatestVolume = 0

'Clear existing data
ws.Range("I1" & ":L" & LastTickerRow).Value = ""
ws.Range("P2:Q4").Value = ""

'Clear the formatting
ws.Range("I2" & ":L" & LastTickerRow).Interior.ColorIndex = 0

'Set the headers
ws.Range("I1").Value = "Ticker"
ws.Range("J1").Value = "Yearly Change"
ws.Range("K1").Value = "Percent Change"
ws.Range("L1").Value = "Total Volume"

ws.Range("O2").Value = "Greatest % Increase"
ws.Range("O3").Value = "Greatest % Decrease"
ws.Range("O4").Value = "Greatest Total Volume"
ws.Range("P1").Value = "Ticker"
ws.Range("Q1").Value = "Value"

Worksheets(ws.Name).Activate

    For i = 2 To LastTickerRow
        
        'If the ticker in the current row is different than the ticker in the next row we are finished processing a broup of tickers.
        'All the calculations for this group are written to the sheet just prior to moving on to the next group.
        If ws.Cells(i, 1).Value <> ws.Cells(i + 1, 1).Value Then
            
            'Set the Ticker
            Ticker = ws.Cells(i, 1).Value
            
            'Set the volume for the ticker that day
            DailyVolume = ws.Cells(i, 7).Value
            
            'Set the final subtotal
            TickerVolumeSubtotal = TickerVolumeSubtotal + DailyVolume
            
            'Get the opening price at begining of year
            YearOpen = ws.Cells(i - RowsProcessed, 3).Value
            
            'Get the closing price at year end
            YearClose = ws.Cells(i, 6).Value
            
            'Set the Yearly Change
            YearlyChange = YearClose - YearOpen
            
            'Calculate the Percent Change and check for 0
            If YearOpen = 0 Then
                YearlyPercentChange = 0
            Else
                YearlyPercentChange = YearlyChange / YearOpen
            End If
            
            'Once we know the ticker has changed, populate the ticker being totaled
            ws.Cells(TickerSubtotalRow, 9).Value = Ticker
            
            'Populate the Yearly Change
            ws.Cells(TickerSubtotalRow, 10).Value = YearClose - YearOpen
            ws.Cells(TickerSubtotalRow, 10).NumberFormat = "0.00"
            
            'Format the Yearly Change
            If YearlyChange > 0 Then
                ws.Cells(TickerSubtotalRow, 10).Interior.Color = RGB(143, 194, 108)
            ElseIf YearlyChange < 0 Then
                ws.Cells(TickerSubtotalRow, 10).Interior.Color = RGB(235, 79, 79)
            End If
            
            'Populate the % Change
            ws.Cells(TickerSubtotalRow, 11).Value = YearlyPercentChange
            ws.Cells(TickerSubtotalRow, 11).NumberFormat = "0.00%"
            
            'Populate the volume subtotal
            ws.Cells(TickerSubtotalRow, 12).Value = TickerVolumeSubtotal
            ws.Cells(TickerSubtotalRow, 12).NumberFormat = "#,###"
            
            'See if the subtotal is greater than the last
            If TickerVolumeSubtotal >= GreatestVolume Then
                TickerWithGreatestVolume = Ticker
                GreatestVolume = TickerVolumeSubtotal
            End If
            
            'See if the percent change is greater than the last
            If YearlyPercentChange >= GreatestIncrease Then
                TickerWithGreatestIncrease = Ticker
                GreatestIncrease = YearlyPercentChange
            End If
            
            'See if the percent change is less than the last
            If YearlyPercentChange <= GreatestDecrease Then
                TickerWithGreatestDecrease = Ticker
                GreatestDecrease = YearlyPercentChange
            End If
            
            'Increment the subtotal row
            TickerSubtotalRow = TickerSubtotalRow + 1
            
            ' Reset the running total
            TickerVolumeSubtotal = 0
            
            ' Reset the the number of rows processed
            RowsProcessed = 0
                   
        Else 'While the ticker is the same we increment all the counters and subtotals
            
            'Set the volume for the ticker that day
            DailyVolume = ws.Cells(i, 7).Value
            
            'Increment the running total for that ticker
            TickerVolumeSubtotal = TickerVolumeSubtotal + DailyVolume
            
            'Increment the RowsProcessed
            RowsProcessed = RowsProcessed + 1
        
        End If
    
    Next i
    
    'Set the greatest values for the sheet
    ws.Range("P2").Value = TickerWithGreatestIncrease
    ws.Range("Q2").Value = GreatestIncrease
    ws.Range("Q2").NumberFormat = "0.00%"
    
    ws.Range("P3").Value = TickerWithGreatestDecrease
    ws.Range("Q3").Value = GreatestDecrease
    ws.Range("Q3").NumberFormat = "0.00%"
    
    ws.Range("P4").Value = TickerWithGreatestVolume
    ws.Range("Q4").Value = GreatestVolume
    ws.Range("Q4").NumberFormat = "#,###"
    
    'Worksheets(ws.Name).Range("I:L,O:Q").EntireColumn.AutoFit
    ws.Range("I:L,O:Q").EntireColumn.AutoFit

Next ws

End Sub

