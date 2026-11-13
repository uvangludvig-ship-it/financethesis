import AppKit
import Foundation

func build(source: URL, prefix: String) throws {
    let fm = FileManager.default
    let files = try fm.contentsOfDirectory(
        at: source,
        includingPropertiesForKeys: nil
    ).filter { $0.lastPathComponent.hasPrefix("page-") && $0.pathExtension == "jpg" }
     .sorted { $0.lastPathComponent < $1.lastPathComponent }

    let perSheet = 20
    let columns = 4
    for start in stride(from: 0, to: files.count, by: perSheet) {
        let end = min(start + perSheet, files.count)
        let chunk = Array(files[start..<end])
        guard let sample = NSImage(contentsOf: chunk[0]) else { continue }
        let pageWidth = sample.size.width
        let pageHeight = sample.size.height
        let labelHeight: CGFloat = 20
        let rows = Int(ceil(Double(chunk.count) / Double(columns)))
        let canvas = NSImage(size: NSSize(
            width: CGFloat(columns) * pageWidth,
            height: CGFloat(rows) * (pageHeight + labelHeight)
        ))

        canvas.lockFocus()
        NSColor.white.setFill()
        NSRect(origin: .zero, size: canvas.size).fill()

        for (index, file) in chunk.enumerated() {
            guard let image = NSImage(contentsOf: file) else { continue }
            let column = index % columns
            let row = index / columns
            let x = CGFloat(column) * pageWidth
            let y = canvas.size.height - CGFloat(row + 1) * (pageHeight + labelHeight)
            image.draw(in: NSRect(x: x, y: y + labelHeight, width: pageWidth, height: pageHeight))
            let label = "Page \(start + index + 1)" as NSString
            label.draw(
                at: NSPoint(x: x + 4, y: y + 3),
                withAttributes: [
                    .font: NSFont.systemFont(ofSize: 11),
                    .foregroundColor: NSColor.black
                ]
            )
        }
        canvas.unlockFocus()

        guard
            let tiff = canvas.tiffRepresentation,
            let bitmap = NSBitmapImageRep(data: tiff),
            let jpeg = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.88])
        else { continue }

        let sheet = start / perSheet + 1
        let output = source.deletingLastPathComponent()
            .appendingPathComponent("\(prefix)_contact_\(sheet).jpg")
        try jpeg.write(to: output)
    }
}

let base = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
try build(source: base.appendingPathComponent("course"), prefix: "course")
try build(source: base.appendingPathComponent("lecture1"), prefix: "lecture1")
