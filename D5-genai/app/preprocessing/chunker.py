from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkConfig:

    chunk_size: int = 800
    overlap: int = 120

    def __post_init__(self) -> None:

        if self.chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0"
            )

        if self.overlap < 0:
            raise ValueError(
                "overlap cannot be negative"
            )

        if self.overlap >= self.chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )


def split_long_block(
    block: str,
    chunk_size: int,
) -> list[str]:

    words = block.split()

    pieces = []

    current_words = []
    current_length = 0

    for word in words:

        additional_length = len(word)

        if current_words:
            additional_length += 1

        if (
            current_length + additional_length
            > chunk_size
        ):

            if current_words:

                pieces.append(
                    " ".join(current_words)
                )

            current_words = [word]
            current_length = len(word)

        else:

            current_words.append(word)
            current_length += additional_length

    if current_words:

        pieces.append(
            " ".join(current_words)
        )

    return pieces


def chunk_text(
    text: str,
    config: ChunkConfig,
) -> list[str]:

    """
    Heading-aware chunking.

    Paragraphs/headings are kept together whenever possible.
    Very large blocks are split safely.
    """

    text = text.strip()

    if not text:
        return []

    blocks = [
        block.strip()
        for block in text.split("\n\n")
        if block.strip()
    ]

    normalized_blocks: list[str] = []

    for block in blocks:

        if len(block) <= config.chunk_size:

            normalized_blocks.append(block)

        else:

            normalized_blocks.extend(
                split_long_block(
                    block,
                    config.chunk_size,
                )
            )

    chunks: list[str] = []

    current_blocks: list[str] = []
    current_length = 0

    for block in normalized_blocks:

        block_length = len(block)

        separator_length = (
            2 if current_blocks else 0
        )

        proposed_length = (
            current_length
            + separator_length
            + block_length
        )

        if (
            current_blocks
            and proposed_length > config.chunk_size
        ):

            chunks.append(
                "\n\n".join(
                    current_blocks
                ).strip()
            )

            # Build overlap from the end of
            # the previous chunk.
            overlap_blocks = []

            overlap_length = 0

            for previous_block in reversed(
                current_blocks
            ):

                addition = (
                    len(previous_block)
                    + (
                        2
                        if overlap_blocks
                        else 0
                    )
                )

                if (
                    overlap_length + addition
                    > config.overlap
                ):
                    break

                overlap_blocks.insert(
                    0,
                    previous_block,
                )

                overlap_length += addition

            current_blocks = (
                overlap_blocks
                + [block]
            )

            current_length = sum(
                len(item)
                for item in current_blocks
            ) + max(
                0,
                (len(current_blocks) - 1) * 2,
            )

        else:

            current_blocks.append(block)

            current_length = (
                proposed_length
            )

    if current_blocks:

        chunks.append(
            "\n\n".join(
                current_blocks
            ).strip()
        )

    return [
        chunk
        for chunk in chunks
        if chunk.strip()
    ]