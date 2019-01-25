import tables
import settings
from os.path import isfile
from game.save.descriptor.superchunk import SuperChunkDescriptor, LoadedChunksDescriptor, ChunkSeedsDescriptor
from game.save.descriptor.chunk import ChunkDescriptor, LoadedMapsDescriptor


def create_ecs_group():
    h5 = None
    if isfile(settings.SAVE_FILE):
        h5 = tables.open_file(settings.SAVE_FILE, mode='a', title='Save')
    else:
        h5 = tables.open_file(settings.SAVE_FILE, mode='w', title='Save')

    def _create_ecs(h5):
        if "frozen" not in h5.root.ecs:
            frozen = h5.create_group("/ecs", "frozen", "Frozen entities")
        if "superchunk" not in h5.root.ecs.frozen:
            superchunk_frozen = h5.create_group("/ecs/frozen", "superchunk", "Frozen superchunks")
        if "chunk" not in h5.root.ecs.frozen.superchunk:
            chunk_frozen = h5.create_group("/ecs/frozen/superchunk", "chunk", "Frozen chunks")
        if "map" not in h5.root.ecs.frozen.superchunk.chunk:
            map_frozen = h5.create_group("/ecs/frozen/superchunk/chunk", "map", "Frozen maps")
        if "vicinity" not in h5.root.ecs.frozen.superchunk.chunk.map:
            vicinity_frozen = h5.create_group("/ecs/frozen/superchunk/chunk/map", "vicinity", "Frozen vicinities")
        if "static_actor" not in h5.root.ecs.frozen.superchunk.chunk.map.vicinity:
            static_actor_frozen = h5.create_group("/ecs/frozen/superchunk/chunk/map/vicinity", "static_actor", "Frozen staic actors")
        if "actor" not in h5.root.ecs.frozen.superchunk.chunk.map.vicinity:
            actor_frozen = h5.create_group("/ecs/frozen/superchunk/chunk/map/vicinity", "actor", "Frozen actors")

        if "hot" not in h5.root.ecs:
            hot = h5.create_group("/ecs", "hot", "Hot entities")
        if "superchunk" not in h5.root.ecs.hot:
            superchunk_hot = h5.create_group("/ecs/hot", "superchunk", "Hot superchunks")
        if "chunk" not in h5.root.ecs.hot.superchunk:
            chunk_hot = h5.create_group("/ecs/hot/superchunk", "chunk", "Hot chunks")
        if "map" not in h5.root.ecs.hot.superchunk.chunk:
            map_hot = h5.create_group("/ecs/hot/superchunk/chunk", "map", "Hot maps")
        if "vicinity" not in h5.root.ecs.hot.superchunk.chunk.map:
            vicinity_hot = h5.create_group("/ecs/hot/superchunk/chunk/map", "vicinity", "Hot vicinities")
        if "static_actor" not in h5.root.ecs.hot.superchunk.chunk.map.vicinity:
            static_actor_hot = h5.create_group("/ecs/hot/superchunk/chunk/map/vicinity", "static_actor", "Hot staic actors")
        if "actor" not in h5.root.ecs.hot.superchunk.chunk.map.vicinity:
            actor_hot = h5.create_group("/ecs/hot/superchunk/chunk/map/vicinity", "actor", "Hot actors")

    if "ecs" in h5.root:
        _create_ecs(h5)
    else:
        ecs = h5.create_group("/", "ecs", "Entity component system descriptor")
        _create_ecs(h5)

    h5.close()

def create_ecs_descriptors():
    h5 = None
    if isfile(settings.SAVE_FILE):
        h5 = tables.open_file(settings.SAVE_FILE, mode='a', title="Save")
        ecs = h5.get_node("/ecs")
        frozen_superchunk = h5.get_node(ecs.frozen.superchunk)
        frozen_chunk = h5.get_node(ecs.frozen.superchunk.chunk)
        frozen_map = h5.get_node(ecs.frozen.superchunk.chunk.map)
        frozen_vicinity = h5.get_node(ecs.frozen.superchunk.chunk.map.vicinity)
        hot_superchunk = h5.get_node(ecs.hot.superchunk)
        hot_chunk = h5.get_node(ecs.hot.superchunk.chunk)
        hot_map = h5.get_node(ecs.hot.superchunk.chunk.map)
        hot_vicinity = h5.get_node(ecs.hot.superchunk.chunk.map.vicinity)

        if "superchunk_descriptor" not in frozen_superchunk:
            frozen_superchunk_descriptor = h5.create_table(frozen_superchunk, "superchunk_descriptor", SuperChunkDescriptor,
                                                           "Super chunk descriptor")
        if "loadedchunks_descriptor" not in frozen_superchunk:
            frozen_loadedchunks_descriptor = h5.create_table(frozen_superchunk, "loadedchunks_descriptor", LoadedChunksDescriptor,
                                                             "Loaded chunks descriptor")
        if "chunkseeds_descriptor" not in frozen_superchunk:
            frozen_chunkseeds_descriptor = h5.create_table(frozen_superchunk, "chunkseeds_descriptor", ChunkSeedsDescriptor,
                                                           "Chunk seeds descriptor")

        if "chunk_descriptor" not in frozen_chunk:
            frozen_chunk_descriptor = h5.create_table(frozen_chunk, "chunk_descriptor", ChunkDescriptor, "Chunk descriptor")

        if "loadedmaps_descriptor" not in frozen_chunk:
            frozen_maps_descriptor = h5.create_table(frozen_chunk, "loadedmaps_descriptor", LoadedMapsDescriptor, "Loaded maps descriptor")



        if "superchunk_descriptor" not in hot_superchunk:
            hot_superchunk_descriptor = h5.create_table(hot_superchunk, "superchunk_descriptor", SuperChunkDescriptor,
                                                           "Super chunk descriptor")
        if "loadedchunks_descriptor" not in hot_superchunk:
            hot_loadedchunks_descriptor = h5.create_table(hot_superchunk, "loadedchunks_descriptor", LoadedChunksDescriptor,
                                                             "Loaded chunks descriptor")
        if "chunkseeds_descriptor" not in hot_superchunk:
            hot_chunkseeds_descriptor = h5.create_table(hot_superchunk, "chunkseeds_descriptor", ChunkSeedsDescriptor,
                                                           "Chunk seeds descriptor")

        if "chunk_descriptor" not in hot_chunk:
            hot_chunk_descriptor = h5.create_table(hot_chunk, "chunk_descriptor", ChunkDescriptor, "Chunk descriptor")

        if "loadedmaps_descriptor" not in hot_chunk:
            hot_maps_descriptor = h5.create_table(hot_chunk, "loadedmaps_descriptor", LoadedMapsDescriptor, "Loaded maps descriptor")

if __name__ == '__main__':
    create_ecs_group()
    create_ecs_descriptors()