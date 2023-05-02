def findChannelBounds(countOfXDivisions, countOfYDivisions):
    channelPositions = []
    for yChan in range(countOfYDivisions):
        row = []
        for xChan in range(countOfXDivisions):
            xPos = xChan * (30 / countOfXDivisions)
            yPos = yChan * (40 / countOfYDivisions)
            row.append((yPos, xPos))
        channelPositions.append(row)
    
    return channelPositions

print(findChannelBounds(3, 4))
