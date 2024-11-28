from enum import Enum, auto


# Requiring that every subclass of BaseEnum contain the 'unknown' member is not ideal, but only a few enumerations
# are planned here. If needed in the future, consider using the functional API to create enumerations on-the-fly. e.g.:
# members = ['amused', 'angry', ...]
# members.append('unknown')
# Emotion = BaseEnum('Emotion', members)
class BaseEnum(Enum):
    """This class contains a factory method that is useful for parsing strings into enumerations and also customizes the
    output of 'auto()' so that negative integer values can be manually specified for aliases. Enumerations extending
    this class must define a member named 'unknown'"""

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return count+1  # ensures that negative values are never auto-generated

    @classmethod
    def create(cls, name):
        try:
            return cls[name]
        except KeyError:
            enum_name = cls.__name__
            print('WARNING! Unknown ' + enum_name + ' "' + name + '". Substituting ' + enum_name + '.unknown.')
            return cls['unknown']


class Character(BaseEnum):
    ahuizotl = auto()
    akyearling = auto()
    applebloom = auto()
    applejack = auto()
    auntholiday = auto()
    auntielofty = auto()
    babsseed = auto()
    barleybarrel = auto()
    bigdaddymccolt = auto()
    bigmac = auto()
    blaze = auto()
    bowhothoof = auto()
    braeburn = auto()
    bulkbiceps = auto()
    caballeron = -1  # alias of drcaballeron
    cadance = auto()
    celestia = auto()
    cheerilee = auto()
    cheesesandwich = auto()
    cherryberry = auto()
    cherryjubilee = auto()
    chrysalis = auto()
    clearsky = auto()
    cloudyquartz = auto()
    cocopommel = auto()
    coriandercumin = auto()
    countesscoloratura = auto()
    cozyglow = auto()
    cranky = auto()
    daybreaker = auto()
    derpy = auto()
    diamondtiara = auto()
    discord = auto()
    donutjoe = auto()
    doublediamond = auto()
    dragonlordtorch = auto()
    drcaballeron = -1  # alias of caballeron
    drfauna = auto()
    drhooves = auto()
    ember = auto()
    fancypants = auto()
    featherweight = auto()
    filthyrich = auto()
    flam = auto()
    flashmagnus = auto()
    fleetfoot = auto()
    flim = auto()
    flurry = -2  # alias of flurryheart
    flurryheart = -2  # alias of flurry
    fluttershy = auto()
    gabby = auto()
    gallus = auto()
    garble = auto()
    gilda = auto()
    gladmane = auto()
    goldiedelicious = auto()
    grampagruff = auto()
    grannysmith = auto()
    grogar = auto()
    gustavelegrand = auto()
    highwinds = auto()
    hoitytoity = auto()
    igneous = auto()
    ironwill = auto()
    kerfuffle = auto()
    lemonhearts = auto()
    lighthoof = auto()
    lightningdust = auto()
    limestone = auto()
    luna = auto()
    lyraheartstrings = auto()
    mahooffield = auto()
    maneallgood = auto()
    maneiac = auto()
    marble = auto()
    matilda = auto()
    maud = auto()
    mayormare = auto()
    mayorsunnyskies = auto()
    meadowbrook = auto()
    minuette = auto()
    missharshwhinny = auto()
    mistmane = auto()
    mistyfly = auto()
    moodyroot = -3  # alias of mrmoodyroot
    moondancer = auto()
    mrcake = auto()
    mrhoofington = auto()
    mrshoofington = auto()
    mrmoodyroot = -3  # alias of moodyroot
    mrscake = auto()
    mrshy = auto()
    mrsshy = auto()
    mudbriar = auto()
    muliamild = auto()
    multiple = auto()
    neighsay = auto()
    nightglider = auto()
    nightlight = auto()
    nightmaremoon = auto()
    ocellus = auto()
    octavia = auto()
    orchardblossom = auto()
    partyfavor = auto()
    petunia = -4  # alias of petuniapetals
    petuniapetals = -4  # alias of petunia
    pharynx = auto()
    photofinish = auto()
    picklebarrel = auto()
    pinkie = auto()
    pipsqueak = auto()
    ponyofshadows = auto()
    princerutherford = auto()
    purseypink = auto()
    quibblepants = auto()
    rainbow = auto()
    rarity = auto()
    rockhoof = auto()
    rollingthunder = auto()
    rose = auto()
    rumble = auto()
    saffronmasala = auto()
    sandbar = auto()
    sanssmirk = auto()
    sapphireshores = auto()
    sassysaddles = auto()
    scootaloo = auto()
    seaspray = auto()
    shimmyshake = auto()
    shiningarmor = auto()
    shortfuse = auto()
    silverspoon = auto()
    silverstream = auto()
    skeedaddle = auto()
    skybeak = auto()
    sludge = auto()
    smolder = auto()
    snails = auto()
    snapshutter = auto()
    snips = auto()
    soarin = auto()
    sombra = auto()
    somnambula = auto()
    spike = auto()
    spitfire = auto()
    spoiledrich = auto()
    starlight = auto()
    starswirl = auto()
    steve = auto()
    stormyflare = auto()
    stygian = auto()
    sugarbelle = auto()
    sunburst = auto()
    surprise = auto()
    svengallop = auto()
    sweetiebelle = auto()
    sweetiedrops = auto()
    terramar = auto()
    thorax = auto()
    thunderlane = auto()
    tirek = auto()
    torquewrench = auto()
    treehugger = auto()
    treeofharmony = auto()
    trixie = auto()
    twilight = auto()
    twilightvelvet = auto()
    twinkleshine = auto()
    twist = auto()
    windrider = auto()
    windsprint = auto()
    windywhistles = auto()
    yona = auto()
    zecora = auto()
    zephyr = auto()
    zestygourmand = auto()

    # obligatory 'unknown'
    unknown = auto()


class Emotion(BaseEnum):
    # official
    amused = auto()
    angry = auto()
    annoyed = auto()
    anxious = auto()
    confused = auto()
    crazy = auto()
    disgusted = -1  # alias of 'disgust'
    fear = auto()
    happy = auto()
    neutral = auto()
    sad = auto()
    sarcastic = auto()
    shouting = auto()
    smug = auto()
    surprised = auto()
    tired = auto()
    whining = auto()
    whispering = auto()

    # unofficial
    disgust = -1  # alias of 'disgusted'
    canterlotvoice = auto()
    love = auto()
    singing = auto()

    # obligatory 'unknown'
    unknown = auto()


class Noise(BaseEnum):
    nothing = auto()
    noisy = auto()
    verynoisy = auto()

    # obligatory 'unknown'
    unknown = auto()
